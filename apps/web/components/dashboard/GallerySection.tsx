'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { getGalleryImages, uploadGalleryImage, deleteGalleryImage, reorderGalleryImages } from '@/lib/provider-api';
import type { GalleryImage } from '@/types/provider';

interface GallerySectionProps {
  token: string;
  t: (key: string) => string;
}

const MAX_IMAGES = 8;

export default function GallerySection({ token, t }: GallerySectionProps) {
  const [images, setImages] = useState<GalleryImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [draggedIndex, setDraggedIndex] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadImages = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getGalleryImages(token);
      setImages(data.sort((a, b) => a.position - b.position));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load gallery');
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    loadImages();
  }, [loadImages]);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    if (images.length + files.length > MAX_IMAGES) {
      setError(t('gallery_max_reached') || 'Maximum number of images reached');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      for (const file of Array.from(files)) {
        const newImage = await uploadGalleryImage(token, file);
        setImages(prev => [...prev, newImage].sort((a, b) => a.position - b.position));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  }

  async function handleDelete(imageId: number) {
    if (!confirm(t('gallery_delete_confirm'))) return;

    try {
      await deleteGalleryImage(token, imageId);
      setImages(prev => prev.filter(img => img.id !== imageId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed');
    }
  }

  function handleDragStart(index: number) {
    setDraggedIndex(index);
  }

  function handleDragOver(e: React.DragEvent) {
    e.preventDefault();
  }

  function handleDrop(e: React.DragEvent, dropIndex: number) {
    e.preventDefault();
    if (draggedIndex === null || draggedIndex === dropIndex) return;

    const newImages = [...images];
    const [draggedItem] = newImages.splice(draggedIndex, 1);
    if (!draggedItem) return;
    newImages.splice(dropIndex, 0, draggedItem);

    const reorderedImages = newImages.map((img, idx) => ({ ...img, position: idx }));
    setImages(reorderedImages);

    const order = reorderedImages.map(img => ({ id: img.id, position: img.position }));
    reorderGalleryImages(token, order).catch(err => {
      setError(err instanceof Error ? err.message : 'Reorder failed');
      loadImages();
    });

    setDraggedIndex(null);
  }

  function handleDragEnd() {
    setDraggedIndex(null);
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <div className="flex items-center justify-center py-8">
          <div className="w-6 h-6 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
      <div>
        <h2 className="text-sm font-semibold text-gray-800">{t('gallery_title')}</h2>
        <p className="text-xs text-gray-500 mt-0.5">{t('gallery_subtitle')}</p>
      </div>

      {images.length === 0 ? (
        <div className="text-center py-8 text-gray-400 text-sm">
          {t('gallery_empty')}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {images.map((image, index) => (
            <div
              key={image.id}
              draggable
              onDragStart={() => handleDragStart(index)}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, index)}
              onDragEnd={handleDragEnd}
              className={`relative aspect-square rounded-lg overflow-hidden bg-gray-100 cursor-move ${
                draggedIndex === index ? 'opacity-50' : ''
              }`}
            >
              <img
                src={image.url}
                alt={`Gallery image ${index + 1}`}
                className="w-full h-full object-cover"
              />
              <button
                type="button"
                onClick={() => handleDelete(image.id)}
                className="absolute top-2 right-2 w-6 h-6 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center text-xs"
              >
                ✕
              </button>
              {image.position === 0 && (
                <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs px-2 py-1 text-center">
                  🖼 {t('gallery_cover_hint')}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          onChange={handleFileChange}
          className="hidden"
        />
        {images.length < MAX_IMAGES ? (
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            className="px-4 py-2 border border-gray-300 text-gray-600 hover:bg-gray-100 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            {uploading ? t('gallery_uploading') : t('gallery_upload_btn')}
          </button>
        ) : (
          <p className="text-xs text-gray-400">{t('gallery_max_reached')}</p>
        )}
        <p className="text-xs text-gray-400 mt-1">{t('gallery_drag_hint')}</p>
      </div>

      {error && (
        <p className="text-xs text-red-600">{error}</p>
      )}
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';

interface RotatingCategoryProps {
  categories?: string[];
}

export default function RotatingCategory({ categories = ["Masaż", "Sprzątanie", "Hydraulik"] }: RotatingCategoryProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsVisible(false);
      
      setTimeout(() => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % categories.length);
        setIsVisible(true);
      }, 300);
    }, 3000);

    return () => clearInterval(interval);
  }, [categories.length]);

  return (
    <span className={`inline-block transition-opacity duration-300 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      {categories[currentIndex]}
    </span>
  );
}

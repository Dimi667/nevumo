'use client';
import { useEffect } from 'react';
import { setCtx } from '@/lib/ctx';

interface Props {
  city?: string;
  category?: string;
}

export default function CtxCapture({ city, category }: Props) {
  useEffect(() => {
    const update: { city?: string; category?: string } = {};
    if (city) update.city = city;
    if (category) update.category = category;
    if (Object.keys(update).length > 0) setCtx(update);
  }, [city, category]);
  return null;
}

import LeadForm from '../../../../../components/LeadForm';
import { notFound } from 'next/navigation';

export async function generateMetadata(props: { params: Promise<{ lang: string, slug: string }> }) {
  const params = await props.params;
  const { lang } = params;
  const parts = params.slug.split('-');
  const id = parts[parts.length - 1];

  try {
    const res = await fetch(`http://127.0.0.1:8000/provider-info/${id}?lang=${encodeURIComponent(lang)}`, { cache: 'no-store' });
    if (!res.ok) return { title: 'Nevumo' };
    const provider = await res.json();
    return { title: `${provider.name} | ${provider.category} | Nevumo` };
  } catch { return { title: 'Nevumo' }; }
}

export default async function Page(props: { params: Promise<{ lang: string, slug: string }> }) {
  const params = await props.params;
  const { lang, slug } = params;

  if (!slug) return notFound();

  const parts = slug.split('-');
  const id = parts[parts.length - 1];

  try {
    const [providerRes, transRes] = await Promise.all([
      fetch(`http://127.0.0.1:8000/provider-info/${id}?lang=${encodeURIComponent(lang)}`, { cache: 'no-store' }),
      fetch(`http://127.0.0.1:8000/translations/${lang}`, { cache: 'no-store' })
    ]);

    if (!providerRes.ok) return notFound();

    const provider = await providerRes.json();
    const translations = await transRes.json();

    return (
      <main>
        <LeadForm initialProvider={provider} initialT={translations} currentLang={lang} />
      </main>
    );
  } catch (e) {
    return <div>Грешка при зареждане.</div>;
  }
}

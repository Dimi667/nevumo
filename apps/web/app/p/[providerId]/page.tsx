import { notFound, permanentRedirect } from 'next/navigation';
import { getProviderById } from '@/lib/api';

type StableProviderRouteParams = {
  providerId: string;
};

export default async function StableProviderRedirectPage(props: {
  params: Promise<StableProviderRouteParams>;
}) {
  const { providerId } = await props.params;
  const provider = await getProviderById(providerId);

  if (!provider?.canonical_path) {
    return notFound();
  }

  permanentRedirect(provider.canonical_path);
}

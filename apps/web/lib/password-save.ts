export async function saveCredentials(email: string, password: string): Promise<void> {
  if (typeof window === 'undefined' || !navigator.credentials) return;
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const CredClass = (window as any).PasswordCredential;
    if (!CredClass) return;
    const cred = new CredClass({ id: email, password, name: email });
    await navigator.credentials.store(cred);
  } catch {
    // Silently ignore
  }
}

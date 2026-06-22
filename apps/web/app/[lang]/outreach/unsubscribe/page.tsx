import Link from 'next/link';

export default async function OutreachUnsubscribePage({
  searchParams,
}: {
  searchParams: Promise<{ confirmed?: string }>;
}) {
  const params = await searchParams;
  const confirmed = params.confirmed === '1';

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center">

        {confirmed ? (
          <>
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              Wypisano pomyślnie
            </h1>
            <p className="text-gray-500 text-base leading-relaxed mb-8">
              Twój adres e-mail został usunięty z listy mailingowej Nevumo.
              Nie będziesz już otrzymywać wiadomości od nas.
            </p>
            <p className="text-sm text-gray-400 mb-6">
              Jeśli chcesz dowiedzieć się więcej o platformie, odwiedź naszą stronę.
            </p>
            <Link
              href="/pl"
              className="inline-block bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-150"
            >
              Przejdź do Nevumo
            </Link>
          </>
        ) : (
          <>
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M12 3a9 9 0 100 18A9 9 0 0012 3z" />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              Nieprawidłowy link
            </h1>
            <p className="text-gray-500 text-base leading-relaxed mb-8">
              Link do wypisania jest nieprawidłowy lub wygasł.
              Jeśli chcesz zrezygnować z otrzymywania wiadomości, napisz do nas.
            </p>
            <a
              href="mailto:privacy@nevumo.com?subject=Rezygnacja+z+mailingów"
              className="inline-block bg-gray-800 hover:bg-gray-900 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-150"
            >
              Napisz do nas
            </a>
          </>
        )}

        <p className="mt-8 text-xs text-gray-300">
          © 2026 Nevumo · FILIPIS CENTAR BALGARIYA OOD · EIK: 175369610
        </p>
      </div>
    </div>
  );
}

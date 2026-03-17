import Link from "next/link";

interface Params {
  params: {
    lang: string;
  };
}

const AVAILABLE_LANGUAGES = [
  "bg",
  "cs",
  "da",
  "de",
  "el",
  "en",
  "es",
  "et",
  "fi",
  "fr",
  "ga",
  "hr",
  "hu",
  "it",
  "lt",
  "lv",
  "mk",
  "mt",
  "nl",
  "no",
  "pl",
  "pt",
  "pt-PT",
  "ro",
  "sk",
  "sl",
  "sq",
  "sr",
  "sv",
  "tr",
];

export default function LangLanding(props: Params) {
  const { lang } = props.params;
  const normalizedLang = AVAILABLE_LANGUAGES.includes(lang) ? lang : "en";

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        gap: "1rem",
        textAlign: "center",
      }}
    >
      <h1>Добре дошли</h1>
      <p>
        Търсите provider страница на език <strong>{normalizedLang}</strong>.
        Изберете една от категориите или отидете директно на примерен доставчик по-долу.
      </p>
      <Link href={`/${normalizedLang}/sofia/massage/maria-petrova-1`}>
        Виж профила на Maria Petrova
      </Link>
    </main>
  );
}

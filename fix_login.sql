-- Изчистване на стари записи за тези ключове, за да няма дублиране
DELETE FROM translations WHERE key IN ('login:heading', 'login:metaTitle', 'login:metaDescription', 'login:footerNote', 'login:featureFree', 'login:featureTime');

INSERT INTO translations (lang, key, value) VALUES
-- Български (bg)
('bg', 'login:heading', 'Намери услуга или започни да предлагаш услуги!'),
('bg', 'login:metaTitle', 'Вход | Nevumo'),
('bg', 'login:metaDescription', 'Намери професионални услуги или предложи своите в Nevumo.'),
('bg', 'login:footerNote', 'Можеш да използваш платформата и по двата начина'),
('bg', 'login:featureFree', '✔ Безплатна регистрация'),
('bg', 'login:featureTime', '✔ Отнема под 1 минута'),

-- English (en)
('en', 'login:heading', 'Find a service or start offering services!'),
('en', 'login:metaTitle', 'Login | Nevumo'),
('en', 'login:metaDescription', 'Find professional services or offer your own on Nevumo.'),
('en', 'login:footerNote', 'You can use the platform both ways'),
('en', 'login:featureFree', '✔ Free registration'),
('en', 'login:featureTime', '✔ Takes less than 1 minute'),

-- Turkish (tr)
('tr', 'login:heading', 'Bir hizmet bulun veya hizmet sunmaya başlayın!'),
('tr', 'login:metaTitle', 'Giriş | Nevumo'),
('tr', 'login:metaDescription', 'Nevumo''da profesyonel hizmetler bulun veya kendi hizmetlerinizi sunun.'),
('tr', 'login:footerNote', 'Platformu her iki şekilde de kullanabilirsiniz'),
('tr', 'login:featureFree', '✔ Ücretsiz kayıt'),
('tr', 'login:featureTime', '✔ 1 dakikadan az sürer'),

-- German (de)
('de', 'login:heading', 'Finden Sie einen Service oder bieten Sie Services an!'),
('de', 'login:metaTitle', 'Login | Nevumo'),
('de', 'login:metaDescription', 'Finden Sie professionelle Dienstleistungen oder bieten Sie Ihre eigenen auf Nevumo an.'),
('de', 'login:footerNote', 'Sie können die Plattform auf beide Arten nutzen'),
('de', 'login:featureFree', '✔ Kostenlose Registrierung'),
('de', 'login:featureTime', '✔ Dauert weniger als 1 Minute'),

-- French (fr)
('fr', 'login:heading', 'Trouvez un service ou commencez à proposer des services !'),
('fr', 'login:metaTitle', 'Connexion | Nevumo'),
('fr', 'login:metaDescription', 'Trouvez des services professionnels ou proposez les vôtres sur Nevumo.'),
('fr', 'login:footerNote', 'Vous pouvez utiliser la plateforme des deux manières'),
('fr', 'login:featureFree', '✔ Inscription gratuite'),
('fr', 'login:featureTime', '✔ Prend moins d''une minute'),

-- Spanish (es)
('es', 'login:heading', '¡Encuentra un servicio o comienza a ofrecer servicios!'),
('es', 'login:metaTitle', 'Iniciar sesión | Nevumo'),
('es', 'login:metaDescription', 'Encuentra servicios profesionales o ofrece los tuyos en Nevumo.'),
('es', 'login:footerNote', 'Puedes usar la plataforma de ambas maneras'),
('es', 'login:featureFree', '✔ Registro gratuito'),
('es', 'login:featureTime', '✔ Toma menos de 1 minuto'),

-- Italian (it)
('it', 'login:heading', 'Trova un servizio o inizia a offrire servizi!'),
('it', 'login:metaTitle', 'Accedi | Nevumo'),
('it', 'login:metaDescription', 'Trova servizi professionali o offri i tuoi su Nevumo.'),
('it', 'login:footerNote', 'Puoi usare la piattaforma in entrambi i modi'),
('it', 'login:featureFree', '✔ Registrazione gratuita'),
('it', 'login:featureTime', '✔ Richiede meno di 1 minuto'),

-- Danish (da)
('da', 'login:heading', 'Find en service eller begynd at tilbyde tjenester!'),
('da', 'login:metaTitle', 'Log ind | Nevumo'),
('da', 'login:metaDescription', 'Find professionelle tjenester eller tilbyd dine egne på Nevumo.'),
('da', 'login:footerNote', 'Du kan bruge platformen på begge måder'),
('da', 'login:featureFree', '✔ Gratis oprettelse'),
('da', 'login:featureTime', '✔ Tager under 1 minut'),

-- Norwegian (no)
('no', 'login:heading', 'Finn en tjeneste eller begynn å tilby tjenester!'),
('no', 'login:metaTitle', 'Logg inn | Nevumo'),
('no', 'login:metaDescription', 'Finn profesjonelle tjenester eller tilby dine egne på Nevumo.'),
('no', 'login:footerNote', 'Du kan bruke plattformen på begge måder'),
('no', 'login:featureFree', '✔ Gratis registrering'),
('no', 'login:featureTime', '✔ Tar under 1 minutt'),

-- Swedish (sv)
('sv', 'login:heading', 'Hitta en tjänst eller börja erbjuda tjänster!'),
('sv', 'login:metaTitle', 'Logga in | Nevumo'),
('sv', 'login:metaDescription', 'Hitta professionella tjänster eller erbjud dina egna på Nevumo.'),
('sv', 'login:footerNote', 'Du kan använda plattformen på båda sätten'),
('sv', 'login:featureFree', '✔ Gratis registrering'),
('sv', 'login:featureTime', '✔ Tar mindre än 1 minut'),

-- Serbian (sr)
('sr', 'login:heading', 'Pronađite uslugu ili počnite da nudite usluge!'),
('sr', 'login:metaTitle', 'Prijava | Nevumo'),
('sr', 'login:metaDescription', 'Pronađite profesionalne usluge ili ponudite svoje na Nevumo platformi.'),
('sr', 'login:footerNote', 'Platformu možete koristiti na oba načina'),
('sr', 'login:featureFree', '✔ Besplatna registracija'),
('sr', 'login:featureTime', '✔ Traje manje od 1 minuta'),

-- Macedonian (mk)
('mk', 'login:heading', 'Најдете услуга или започнете да нудите услуги!'),
('mk', 'login:metaTitle', 'Најава | Nevumo'),
('mk', 'login:metaDescription', 'Најдете професионални услуги или понудете ги вашите на Nevumo.'),
('mk', 'login:footerNote', 'Можете да ја користите платформата на двата начини'),
('mk', 'login:featureFree', '✔ Бесплатна регистрација'),
('mk', 'login:featureTime', '✔ Одзема помалку од 1 минута'),

-- Greek (el)
('el', 'login:heading', 'Βρείτε μια υπηρεσία ή αρχίστε να προσφέρετε υπηρεσίες!'),
('el', 'login:metaTitle', 'Σύνδεση | Nevumo'),
('el', 'login:metaDescription', 'Βρείτε επαγγελματικές υπηρεσίες ή προσφέρετε τις δικές σας στο Nevumo.'),
('el', 'login:footerNote', 'Μπορείτε να χρησιμοποιήσετε την πλατφόρμα και με τους δύο τρόπους'),
('el', 'login:featureFree', '✔ Δωρεάν εγγραφή'),
('el', 'login:featureTime', '✔ Χρειάζεται λιγότερο από 1 λεπτό'),

-- Romanian (ro)
('ro', 'login:heading', 'Găsește un serviciu sau începe să oferi servicii!'),
('ro', 'login:metaTitle', 'Autentificare | Nevumo'),
('ro', 'login:metaDescription', 'Găsește servicii profesionale sau oferă-le pe ale tale pe Nevumo.'),
('ro', 'login:footerNote', 'Poți folosi platforma în ambele moduri'),
('ro', 'login:featureFree', '✔ Înregistrare gratuită'),
('ro', 'login:featureTime', '✔ Durează mai puțin de 1 minut'),

-- Polish (pl)
('pl', 'login:heading', 'Znajdź usługę lub zacznij oferować usługi!'),
('pl', 'login:metaTitle', 'Logowanie | Nevumo'),
('pl', 'login:metaDescription', 'Znajdź profesjonalne usługi lub oferuj własne na Nevumo.'),
('pl', 'login:footerNote', 'Możesz korzystarć z platformy na oba sposoby'),
('pl', 'login:featureFree', '✔ Bezpłatna rejestracja'),
('pl', 'login:featureTime', '✔ Zajmuje mniej niż 1 minutę'),

-- Portuguese (pt)
('pt', 'login:heading', 'Encontre um serviço ou comece a oferecer serviços!'),
('pt', 'login:metaTitle', 'Entrar | Nevumo'),
('pt', 'login:metaDescription', 'Encontre serviços profissionais ou ofereça os seus no Nevumo.'),
('pt', 'login:footerNote', 'Pode utilizar a plataforma de ambas as formas'),
('pt', 'login:featureFree', '✔ Registo gratuito'),
('pt', 'login:featureTime', '✔ Demora menos de 1 minuto'),

-- Dutch (nl)
('nl', 'login:heading', 'Vind een dienst of begin met het aanbieden van diensten!'),
('nl', 'login:metaTitle', 'Inloggen | Nevumo'),
('nl', 'login:metaDescription', 'Vind professionele diensten of bied uw eigen diensten aan op Nevumo.'),
('nl', 'login:footerNote', 'U kunt het platform op beide manieren gebruiken'),
('nl', 'login:featureFree', '✔ Gratis registratie'),
('nl', 'login:featureTime', '✔ Duurt minder dan 1 minuut'),

-- Finnish (fi)
('fi', 'login:heading', 'Löydä palvelu tai ala tarjota palveluita!'),
('fi', 'login:metaTitle', 'Kirjaudu sisään | Nevumo'),
('fi', 'login:metaDescription', 'Löydä ammattipalveluita tai tarjoa omia palveluitasi Nevumossa.'),
('fi', 'login:footerNote', 'Voit käyttää alustaa molemmin tavoin'),
('fi', 'login:featureFree', '✔ Ilmainen rekisteröityminen'),
('fi', 'login:featureTime', '✔ Kestää alle minuutin'),

-- Czech (cs)
('cs', 'login:heading', 'Najděte službu nebo začněte nabízet služby!'),
('cs', 'login:metaTitle', 'Přihlášení | Nevumo'),
('cs', 'login:metaDescription', 'Najděte profesionální služby nebo nabídněte své vlastní na Nevumo.'),
('cs', 'login:footerNote', 'Platformu můžete používat oběma způsoby'),
('cs', 'login:featureFree', '✔ Bezplatná registrace'),
('cs', 'login:featureTime', '✔ Trvá méně než 1 minutu'),

-- Slovak (sk)
('sk', 'login:heading', 'Nájdite službu alebo začnite ponúkať služby!'),
('sk', 'login:metaTitle', 'Prihlásenie | Nevumo'),
('sk', 'login:metaDescription', 'Nájdite profesionálne služby alebo ponúknite svoje vlastné na Nevumo.'),
('sk', 'login:footerNote', 'Platformu môžete používať oboma spôsobmi'),
('sk', 'login:featureFree', '✔ Bezplatná registrácia'),
('sk', 'login:featureTime', '✔ Trvá menej ako 1 minútu'),

-- Hungarian (hu)
('hu', 'login:heading', 'Keressen szolgáltatást vagy kezdjen el szolgáltatásokat kínálni!'),
('hu', 'login:metaTitle', 'Belépés | Nevumo'),
('hu', 'login:metaDescription', 'Keressen professzionális szolgáltatásokat vagy kínálja sajátjait a Nevumo-n.'),
('hu', 'login:footerNote', 'A platformot mindkét módon használhatja'),
('hu', 'login:featureFree', '✔ Ingyenes regisztráció'),
('hu', 'login:featureTime', '✔ Kevesebb mint 1 percet vesz igénybe'),

-- Estonian (et)
('et', 'login:heading', 'Leia teenus või hakka teenuseid pakkuma!'),
('et', 'login:metaTitle', 'Logi sisse | Nevumo'),
('et', 'login:metaDescription', 'Leia professionaalseid teenuseid või paku oma teenuseid Nevumos.'),
('et', 'login:footerNote', 'Saate platvormi kasutada mõlemal viisil'),
('et', 'login:featureFree', '✔ Tasuta registreerimine'),
('et', 'login:featureTime', '✔ Võtab vähem kui 1 minuti'),

-- Latvian (lv)
('lv', 'login:heading', 'Atrodiet pakalpojumu vai sāciet piedāvāt pakalpojumus!'),
('lv', 'login:metaTitle', 'Pieteikties | Nevumo'),
('lv', 'login:metaDescription', 'Atrodiet profesionālus pakalpojumus vai piedāvājiet savus Nevumo.'),
('lv', 'login:footerNote', 'Platformu varat izmantot abos veidos'),
('lv', 'login:featureFree', '✔ Bezmaksas reģistrācija'),
('lv', 'login:featureTime', '✔ Aizņem mazāk par 1 minūti'),

-- Lithuanian (lt)
('lt', 'login:heading', 'Raskite paslaugą arba pradėkite siūlyti paslaugas!'),
('lt', 'login:metaTitle', 'Prisijungti | Nevumo'),
('lt', 'login:metaDescription', 'Raskite profesionalių paslaugų arba siūlykite savo Nevumo platformoje.'),
('lt', 'login:footerNote', 'Platforma galite naudotis abiem būdais'),
('lt', 'login:featureFree', '✔ Nemokama registracija'),
('lt', 'login:featureTime', '✔ Užtrunka mažiau nei 1 minutę'),

-- Slovenian (sl)
('sl', 'login:heading', 'Poiščite storitev ali začnite ponujati storitve!'),
('sl', 'login:metaTitle', 'Prijava | Nevumo'),
('sl', 'login:metaDescription', 'Poiščite strokovne storitve ali ponudite svoje na Nevumo.'),
('sl', 'login:footerNote', 'Platformo lahko uporabljate na oba načina'),
('sl', 'login:featureFree', '✔ Brezplačna registracija'),
('sl', 'login:featureTime', '✔ Traja manj kot 1 minuto'),

-- Croatian (hr)
('hr', 'login:heading', 'Pronađite uslugu ili počnite nuditi usluge!'),
('hr', 'login:metaTitle', 'Prijava | Nevumo'),
('hr', 'login:metaDescription', 'Pronađite profesionalne usluge ili ponudite svoje na Nevumo platformi.'),
('hr', 'login:footerNote', 'Platformu možete koristiti na oba načina'),
('hr', 'login:featureFree', '✔ Besplatna registracija'),
('hr', 'login:featureTime', '✔ Traje manje od 1 minute'),

-- Albanian (sq)
('sq', 'login:heading', 'Gjeni një shërbim ose filloni të ofroni shërbime!'),
('sq', 'login:metaTitle', 'Hyni | Nevumo'),
('sq', 'login:metaDescription', 'Gjeni shërbime profesionale ose ofroni tuajat në Nevumo.'),
('sq', 'login:footerNote', 'Mund ta përdorni platformën në të dyja mënyrat'),
('sq', 'login:featureFree', '✔ Regjistrim falas'),
('sq', 'login:featureTime', '✔ Zgjat më pak se 1 minutë'),

-- Icelandic (is)
('is', 'login:heading', 'Finndu þjónustu eða byrjaðu að bjóða þjónustu!'),
('is', 'login:metaTitle', 'Innskráning | Nevumo'),
('is', 'login:metaDescription', 'Finndu faglega þjónustu eða bjóddu þína eigin á Nevumo.'),
('is', 'login:footerNote', 'Þú getur notað vettvanginn á báða vegu'),
('is', 'login:featureFree', '✔ Ókeypis skráning'),
('is', 'login:featureTime', '✔ Tekur innan við 1 mínútu'),

-- Irish (ga)
('ga', 'login:heading', 'Faigh seirbhís nó tosú ag tairiscint seirbhísí!'),
('ga', 'login:metaTitle', 'Logáil isteach | Nevumo'),
('ga', 'login:metaDescription', 'Faigh seirbhísí gairmiúla nó tairg do chuid féin ar Nevumo.'),
('ga', 'login:footerNote', 'Is féidir leat an t-ardán a úsáid ar an dá bhealach'),
('ga', 'login:featureFree', '✔ Clárú saor in aisce'),
('ga', 'login:featureTime', '✔ Tógann sé níos lú ná 1 nóiméad'),

-- Maltese (mt)
('mt', 'login:heading', 'Sib servizz jew ibda offri servizzi!'),
('mt', 'login:metaTitle', 'Illogja | Nevumo'),
('mt', 'login:metaDescription', 'Sib servizzi professjonali jew offri tiegħek fuq Nevumo.'),
('mt', 'login:footerNote', 'Tista'' tuża l-pjattaforma miż-żewġ naħat'),
('mt', 'login:featureFree', '✔ Reġistrazzjoni b''xejn'),
('mt', 'login:featureTime', '✔ Jieħu inqas minn minuta')
ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value;
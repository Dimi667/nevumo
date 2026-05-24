#!/usr/bin/env python3
"""
Generate row() format for label_cancelled_leads and label_notes_privacy_disclaimer.
"""

LANGS = ['en', 'bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt', 'lv', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'pt-PT', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'tr', 'uk']

# label_cancelled_leads
cancelled = [
    'Cancelled leads', 'Отказани запитвания', 'Zrušené poptávky', 'Annullerede forespørgsler', 'Stornierte Anfragen', 'Ακυρωμένα αιτήματα', 'Solicitudes canceladas', 'Tühistatud päringud', 'Perutut kyselyt', 'Demandes annulées', 'Iarrataí cealaithe', 'Otkazani upiti', 'Visszavont érdeklődések', 'Afturkallaðar fyrirspurnir', 'Richieste annullate', 'Ofgesot Ufroe', 'Atšaukti užklausos', 'Atceltie pieprasījumi', 'Откажани барања', 'Talbiet mħassra', 'Geannuleerde aanvragen', 'Avbrutte forespørsler', 'Anulowane zapytania', 'Solicitações canceladas', 'Pedidos cancelados', 'Solicitări anulate', 'Отменённые заявки', 'Zrušené dopyty', 'Preklicane povpraševanja', 'Kërkesat e anuluara', 'Otkazani upiti', 'Avbrutna förfrågningar', 'İptal edilen talepler', 'Скасовані запити'
]

# label_notes_privacy_disclaimer
privacy = [
    'Notes are visible only to you', 'Бележките са видими само за Вас', 'Poznámky jsou viditelné pouze pro vás', 'Noter er kun synlige for dig', 'Notizen sind nur für Sie sichtbar', 'Οι σημειώσεις είναι ορατές μόνο σε εσάς', 'Las notas solo son visibles para usted', 'Märkmed on nähtavad ainult teile', 'Muistiinpanot näkyvät vain sinulle', 'Les notes ne sont visibles que par vous', 'Níl nótaí le feiceáil ach agat féin', 'Bilješke su vidljive samo vama', 'A jegyzetek csak Ön számára láthatók', 'Minnismiðar eru aðeins sýnilegir þér', 'Le note sono visibili solo a te', 'Notizen si nëmmen fir Iech siichtbar', 'Pastabos matomos tik jums', 'Piezīmes ir redzamas tikai jums', 'Белешките се видливи само за вас', 'In-noti huma viżibbli biss għalik', 'Notities zijn alleen voor u zichtbaar', 'Notater er bare synlige for deg', 'Notatki są widoczne tylko dla Ciebie', 'As notas são visíveis apenas para você', 'As notas são visíveis apenas para si', 'Notele sunt vizibile doar pentru dvs.', 'Заметки видны только вам', 'Poznámky sú viditeľné iba pre vás', 'Opombe so vidne samo vam', 'Shënimet janë të dukshme vetëm për ju', 'Белешке су видљиве само вама', 'Anteckningar är bara synliga för dig', 'Notlar yalnızca size görünür', 'Нотатки видимі лише вам'
]

print('    "label_cancelled_leads": row(')
for i in range(0, len(cancelled), 8):
    chunk = cancelled[i:i+8]
    print(f'        {", ".join([f"{v}" for v in chunk])},')
print('    ),')
print()
print('    "label_notes_privacy_disclaimer": row(')
for i in range(0, len(privacy), 8):
    chunk = privacy[i:i+8]
    print(f'        {", ".join([f"{v}" for v in chunk])},')
print('    ),')

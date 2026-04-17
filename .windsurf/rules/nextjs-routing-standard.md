NEXT.JS 15+ ROUTING STANDARD
Всяка нова страница (page.tsx) или лейаут (layout.tsx) в apps/web/app/[lang] ЗАДЪЛЖИТЕЛНО трябва да дефинира params и searchParams като Promise.

Директното използване на params.lang без await или React.use() е забранено.

Преводите (t()) се използват БЕЗ namespace префикси (напр. ползвай hero_title, а не homepage.hero_title), тъй като API-то доставя преводите "разопаковани".

Цел: Предотвратяване на 404 грешки и счупени преводи при бъдещо разширяване на проекта.

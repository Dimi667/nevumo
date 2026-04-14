FROM node:22-alpine

WORKDIR /workspace

COPY package.json package-lock.json ./
COPY apps/web/package.json ./apps/web/package.json
COPY apps/docs/package.json ./apps/docs/package.json
COPY packages/eslint-config/package.json ./packages/eslint-config/package.json
COPY packages/typescript-config/package.json ./packages/typescript-config/package.json
COPY packages/ui/package.json ./packages/ui/package.json

RUN npm install

COPY apps/web ./apps/web
COPY packages ./packages

WORKDIR /workspace/apps/web

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
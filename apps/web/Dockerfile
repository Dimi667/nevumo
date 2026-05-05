FROM node:22-slim

WORKDIR /workspace

COPY package.json package-lock.json ./
COPY apps/web/package.json ./apps/web/package.json
COPY apps/docs/package.json ./apps/docs/package.json
COPY packages/eslint-config/package.json ./packages/eslint-config/package.json
COPY packages/typescript-config/package.json ./packages/typescript-config/package.json
COPY packages/ui/package.json ./packages/ui/package.json

RUN npm install

# Copy source code before installing platform-specific dependencies
COPY apps/web ./apps/web
COPY packages ./packages

# Reinstall lightningcss to get the correct platform-specific binary for Debian
RUN npm uninstall lightningcss-linux-x64-musl
RUN npm install

WORKDIR /workspace/apps/web

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
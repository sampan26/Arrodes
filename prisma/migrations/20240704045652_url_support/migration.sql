/*
  Warnings:

  - The values [OPENAI] on the enum `DocumentType` will be removed. If these variants are still used in the database, this will fail.

*/
-- AlterEnum
BEGIN;
CREATE TYPE "DocumentType_new" AS ENUM ('TXT', 'PDF', 'YOUTUBE', 'OPENAPI', 'URL');
ALTER TABLE "Document" ALTER COLUMN "type" DROP DEFAULT;
ALTER TABLE "Document" ALTER COLUMN "type" TYPE "DocumentType_new" USING ("type"::text::"DocumentType_new");
ALTER TYPE "DocumentType" RENAME TO "DocumentType_old";
ALTER TYPE "DocumentType_new" RENAME TO "DocumentType";
DROP TYPE "DocumentType_old";
ALTER TABLE "Document" ALTER COLUMN "type" SET DEFAULT 'TXT';
COMMIT;

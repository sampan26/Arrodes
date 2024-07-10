-- AlterEnum
ALTER TYPE "DocumentType" ADD VALUE 'MARKDOWN';

-- AlterEnum
ALTER TYPE "ToolType" ADD VALUE 'REPLICATE';

-- AlterTable
ALTER TABLE "Tool" ADD COLUMN     "metadata" JSONB;

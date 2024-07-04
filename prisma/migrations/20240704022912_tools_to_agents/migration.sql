-- CreateEnum
CREATE TYPE "ToolType" AS ENUM ('BROWSER', 'SEARCH');

-- AlterEnum
ALTER TYPE "DocumentType" ADD VALUE 'OPENAi';

-- DropForeignKey
ALTER TABLE "Agent" DROP CONSTRAINT "Agent_documentId_fkey";

-- DropForeignKey
ALTER TABLE "Agent" DROP CONSTRAINT "Agent_promptId_fkey";

-- DropForeignKey
ALTER TABLE "AgentMemory" DROP CONSTRAINT "AgentMemory_agentId_fkey";

-- AlterTable
ALTER TABLE "Agent" ADD COLUMN     "toolId" VARCHAR(255);

-- AlterTable
ALTER TABLE "Document" ADD COLUMN     "authorization" JSONB;

-- CreateTable
CREATE TABLE "Tool" (
    "id" VARCHAR(255) NOT NULL,
    "name" TEXT NOT NULL,
    "type" "ToolType",
    "userId" VARCHAR(255) NOT NULL,
    "createdAt" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Tool_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Agent" ADD CONSTRAINT "Agent_documentId_fkey" FOREIGN KEY ("documentId") REFERENCES "Document"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Agent" ADD CONSTRAINT "Agent_toolId_fkey" FOREIGN KEY ("toolId") REFERENCES "Tool"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Agent" ADD CONSTRAINT "Agent_promptId_fkey" FOREIGN KEY ("promptId") REFERENCES "Prompt"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AgentMemory" ADD CONSTRAINT "AgentMemory_agentId_fkey" FOREIGN KEY ("agentId") REFERENCES "Agent"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Tool" ADD CONSTRAINT "Tool_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

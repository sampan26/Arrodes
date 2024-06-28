-- DropForeignKey
ALTER TABLE "Agent" DROP CONSTRAINT "Agent_documentId_fkey";

-- DropForeignKey
ALTER TABLE "AgentMemory" DROP CONSTRAINT "AgentMemory_agentId_fkey";

-- AlterTable
ALTER TABLE "Profile" ADD COLUMN     "metadata" JSONB DEFAULT '{}';

-- AddForeignKey
ALTER TABLE "Agent" ADD CONSTRAINT "Agent_documentId_fkey" FOREIGN KEY ("documentId") REFERENCES "Document"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AgentMemory" ADD CONSTRAINT "AgentMemory_agentId_fkey" FOREIGN KEY ("agentId") REFERENCES "Agent"("id") ON DELETE CASCADE ON UPDATE CASCADE;

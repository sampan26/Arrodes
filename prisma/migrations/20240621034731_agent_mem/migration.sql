-- CreateEnum
CREATE TYPE "AgentMemoryAuthorType" AS ENUM ('HUMAN', 'AI');

-- CreateTable
CREATE TABLE "AgentMemory" (
    "id" VARCHAR(255) NOT NULL,
    "agentId" VARCHAR(255) NOT NULL,
    "author" "AgentMemoryAuthorType" NOT NULL DEFAULT 'HUMAN',
    "message" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP(3),

    CONSTRAINT "AgentMemory_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "AgentMemory" ADD CONSTRAINT "AgentMemory_agentId_fkey" FOREIGN KEY ("agentId") REFERENCES "Agent"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AlterTable
ALTER TABLE "Agent" ADD COLUMN     "hasMemory" BOOLEAN NOT NULL DEFAULT false,
ALTER COLUMN "llm" SET DEFAULT '{ "provider": "openai-chat", "model": "gpt-3.5-turbo" }';

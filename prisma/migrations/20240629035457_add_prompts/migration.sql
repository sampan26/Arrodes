-- CreateTable
CREATE TABLE "Prompts" (
    "id" VARCHAR(255) NOT NULL,
    "name" TEXT NOT NULL,
    "template" TEXT NOT NULL,
    "input_variables" JSONB NOT NULL,
    "userId" VARCHAR(255) NOT NULL,
    "createdAt" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP(3),

    CONSTRAINT "Prompts_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Prompts" ADD CONSTRAINT "Prompts_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

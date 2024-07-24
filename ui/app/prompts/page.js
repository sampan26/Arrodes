import { getServerSession } from "next-auth/next";
import { options } from "@/lib/next-auth";
import PromptsClientPage from "./client-page";
import API from "@/lib/api";

export const metadata = {
  title: "Prompts | Superagent",
  description: "Manage your prompts",
};

export default async function ApiTokens() {
    const session = await getServerSession(options);
    const api = new API(session);
    const prompts = api.getPrompts()

    return <PromptsClientPage data={prompts} session={session} />;
}
import NextAuth from "next-auth"
import { authOptions } from "@/auth";

// https://next-auth.js.org/getting-started/example#add-api-route
const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }

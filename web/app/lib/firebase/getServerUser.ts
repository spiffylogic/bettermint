// https://blog.stackademic.com/setting-up-firebase-authentication-with-next-13-app-router-using-server-components-03fbcab254e4

import { cookies } from "next/headers";
import { customInitApp } from "@/app/lib/firebase/firebase-admin-config";
import { auth } from "firebase-admin";

// I guess this is here to ensure initialization happens before this function is used.
customInitApp()

// Get the user from the session cookie
// if theres no session or its invalid, return null
export default async function getServerUser() {
  const session = cookies().get("session")?.value;
  if (!session) {
    return null;
  }
  const user = await auth().verifySessionCookie(session, true);
  return user;
}

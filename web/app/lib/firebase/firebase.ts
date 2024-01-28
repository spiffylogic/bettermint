// This code was adapted from https://github.com/firebase/friendlyeats-web.git
// which comes from the code lab https://firebase.google.com/codelabs/firebase-nextjs

import { initializeApp, getApps } from "firebase/app";
import { getAuth } from "firebase/auth";

export const firebaseConfig = {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
    authDomain: process.env.NEXT_PUBLIC_AUTH_DOMAIN,
    projectId: process.env.NEXT_PUBLIC_PROJECT_ID,
    appId: process.env.NEXT_PUBLIC_APP_ID
};

export const firebaseApp =
  getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const firebaseAuth = getAuth(firebaseApp);

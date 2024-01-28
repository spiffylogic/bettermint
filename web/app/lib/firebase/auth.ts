// This code was adapted from https://github.com/firebase/friendlyeats-web.git
// which comes from the code lab https://firebase.google.com/codelabs/firebase-nextjs

import {
    GoogleAuthProvider,
    NextOrObserver,
    onAuthStateChanged as _onAuthStateChanged,
    signInWithPopup,
    User,
  } from "firebase/auth";

  import { firebaseAuth } from "@/app/lib/firebase/firebase";

  export function onAuthStateChanged(cb: NextOrObserver<User>) {
      return _onAuthStateChanged(firebaseAuth, cb);
  }

  export async function signInWithGoogle() {
    const provider = new GoogleAuthProvider();

    try {
      await signInWithPopup(firebaseAuth, provider);
    } catch (error) {
      console.error("Error signing in with Google", error);
    }
  }

  export async function signOut() {
    try {
      return firebaseAuth.signOut();
    } catch (error) {
      console.error("Error signing out with Google", error);
    }
  }

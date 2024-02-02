// https://blog.stackademic.com/setting-up-firebase-authentication-with-next-13-app-router-using-server-components-03fbcab254e4

import * as admin from "firebase-admin";
import { initializeApp, getApps, cert } from 'firebase-admin/app';
import serviceAccountJson from '@/service-account.json'

const serviceAccount = serviceAccountJson as admin.ServiceAccount;

const firebaseAdminConfig = {
    credential: cert(serviceAccount)
}

export function customInitApp() {
  if (getApps().length <= 0) {
    return initializeApp(firebaseAdminConfig);
  } else {
    return getApps()[0];
  }
}
export const adminAuth = customInitApp();
import NextAuth from 'next-auth';
import { authConfig } from './auth.config';

// See https://nextjs.org/docs/app/building-your-application/routing/middleware
// The advantage of employing Middleware is that the protected routes will not even start rendering
// until the Middleware verifies the authentication, enhancing both the security and performance of your application.

// Here you're initializing NextAuth.js with the authConfig object and exporting the auth property.
export default NextAuth(authConfig).auth;

// You're also using the matcher option from Middleware to specify that it should run on specific paths.
export const config = {
  // https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
};
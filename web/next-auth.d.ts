import NextAuth from 'next-auth';

// https://stackoverflow.com/a/75466129/432311
// Add id field to user type.
declare module 'next-auth' {
  interface Session {
    user: {
      uid: string;
    } & DefaultSession['user'];
  }
}

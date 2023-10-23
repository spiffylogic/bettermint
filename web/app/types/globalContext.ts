import { Dispatch, SetStateAction } from "react";
import { User } from 'firebase/auth';

export type UserContext = {
    context: UserContext,
    setContext: Dispatch<SetStateAction<UserContext>>,
    user: User | null,
    setUser: Dispatch<SetStateAction<User | null>>
}
import { Dispatch, SetStateAction, createContext, useContext } from 'react';
import { UserContext } from '@/app/lib/globalContext';
const AppContext = createContext({} as UserContext);
export default AppContext;

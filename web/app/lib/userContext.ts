import { Dispatch, SetStateAction, createContext, useContext } from 'react';
import { UserContext } from './globalContext';
const AppContext = createContext({} as UserContext);
export default AppContext;

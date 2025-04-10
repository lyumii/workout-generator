import { createContext, useContext } from "react";

export const ColorContext = createContext<string>("#FFFFFF");

export const usePulseColor = () => useContext(ColorContext);

import { createContext, useContext } from "react";

interface EditContextType {
  editedExercises: {
    [historyId: number]: {
      [exerciseIndex: number]: { sets: number; reps: number };
    };
  };
  setEditedExercises: React.Dispatch<
    React.SetStateAction<{
      [historyId: number]: {
        [exerciseIndex: number]: { sets: number; reps: number };
      };
    }>
  >;
}

export const EditContext = createContext<EditContextType | null>(null);

export const useEditContext = () => {
  const context = useContext(EditContext);
  if (!context)
    throw new Error("useEditContext must be used within EditProvider");
  return context;
};

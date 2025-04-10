import { useContext, createContext } from "react";

export const WorkoutCardContext = createContext<{
  historyId: number;
  exerciseIndex: number;
} | null>(null);
export const useWorkoutCardContext = () => {
  const ctx = useContext(WorkoutCardContext);
  if (!ctx)
    throw new Error(
      "useWorkoutCardContext must be inside WorkoutCardContext.Provider"
    );
  return ctx;
};

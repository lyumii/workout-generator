import { useContext, createContext } from "react";
import { Exercise } from "./WorkoutHistoryItem";

export const WorkoutCardContext = createContext<{
  historyId: number;
  exerciseIndex: number;
  searchTerm: string;
  setSearchTerm: React.Dispatch<React.SetStateAction<string>>;
  searchResults: Exercise[];
  setSearchResults: React.Dispatch<React.SetStateAction<Exercise[]>>;
  // addExerciseToWorkout: (exercise: Exercise) => void;
} | null>(null);
export const useWorkoutCardContext = () => {
  const ctx = useContext(WorkoutCardContext);
  if (!ctx)
    throw new Error(
      "useWorkoutCardContext must be inside WorkoutCardContext.Provider"
    );
  return ctx;
};

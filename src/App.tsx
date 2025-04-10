import BrowseWorkoutHistory from "./BrowseWorkoutHistory";
import ChoiceButtons from "./ChoiceButtons";
import CurrentWorkout from "./CurrentWorkout";
import GenerateWorkout from "./GenerateWorkout";
import Header from "./Header";
import { useMemo, useState } from "react";
import { Route, Routes } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { EditContext } from "./EditContext";

function App() {
  const [editedExercises, setEditedExercises] = useState<{
    [historyId: number]: {
      [exerciseIndex: number]: { sets: number; reps: number };
    };
  }>({});
  return (
    <main className="main">
      <Header>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <ChoiceButtons />
              </>
            }
          />

          <Route
            path="/browse"
            element={
              <EditContext.Provider
                value={{ editedExercises, setEditedExercises }}
              >
                <BrowseWorkoutHistory />
              </EditContext.Provider>
            }
          />

          <Route
            path="/generated"
            element={useMemo(
              () => (
                <GenerateWorkout />
              ),
              []
            )}
          />

          <Route path="/current" element={<CurrentWorkout />} />
        </Routes>
        <Toaster position="top-right" toastOptions={{ duration: 3000 }} />
      </Header>
    </main>
  );
}

export default App;

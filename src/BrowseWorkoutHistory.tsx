import { useState, useEffect } from "react";
import WorkoutHistoryItem, { WorkoutHistoryEntry } from "./WorkoutHistoryItem";
import colors from "./colors";
import { toast } from "react-hot-toast";
import { useEditContext } from "./EditContext";

export default function BrowseWorkoutHistory() {
  const [history, setHistory] = useState<WorkoutHistoryEntry[]>([]);
  const { editedExercises } = useEditContext();

  const deleteWorkoutFromHistory = async (id: number) => {
    try {
      const res = await fetch(`http://localhost:5000/workouthistory/${id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        console.log("Deleted!");
        toast(" Workout deleted!", {
          icon: "💀",
          style: {
            background: "#333",
            color: "#fff",
            border: "1px solid #F5A623",
          },
        });
        setHistory((prev) => prev.filter((entry) => entry.id !== id));
      } else {
        console.error("Failed to delete workout");
      }
    } catch (err) {
      console.error("Error deleting:", err);
    }
  };

  const fetchHistory = async () => {
    const res = await fetch("http://localhost:5000/workouthistory");
    const data = await res.json();
    setHistory(data);
  };

  const submitEdit = async (
    id: number,
    edited: { [index: number]: { sets?: number; reps?: number } }
  ) => {
    console.log("SUBMITTING EDIT:", { id, edited });

    for (const [indexStr, changes] of Object.entries(edited)) {
      const index = Number(indexStr);
      const res = await fetch(`http://localhost:5000/browse/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index, ...changes }),
      });

      if (!res.ok) {
        throw new Error("Failed to update exercise index " + index);
      }
    }
    fetchHistory();
    toast.success("Workout updated!");
  };

  useEffect(() => {
    fetch("http://localhost:5000/workouthistory")
      .then((res) => res.json())
      .then((data) => setHistory(data));
  }, []);
  return (
    <div className="generatedworkoutswidth">
      <div>
        {history.map((entry: WorkoutHistoryEntry, index) => (
          <WorkoutHistoryItem
            key={entry.id}
            entry={entry}
            color={colors[index % colors.length]}
            onDelete={() => deleteWorkoutFromHistory(entry.id)}
            onEdit={(id) => submitEdit(id, editedExercises[id])}
          />
        ))}
      </div>
    </div>
  );
}

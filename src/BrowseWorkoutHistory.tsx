import { useState, useEffect } from "react";
import WorkoutHistoryItem, { WorkoutHistoryEntry } from "./WorkoutHistoryItem";

export default function BrowseWorkoutHistory() {
  const [history, setHistory] = useState<WorkoutHistoryEntry[]>([]);

  useEffect(() => {
    fetch("http://localhost:5000/workouthistory")
      .then((res) => res.json())
      .then((data) => setHistory(data));
  }, []);
  return (
    <div>
      <div>
        {history.map((entry: WorkoutHistoryEntry) => (
          <WorkoutHistoryItem key={entry.id} entry={entry} />
        ))}
      </div>
    </div>
  );
}

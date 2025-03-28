import { useState, useEffect } from "react";
import WorkoutHistoryItem, { WorkoutHistoryEntry } from "./WorkoutHistoryItem";
import colors from "./colors";

export default function BrowseWorkoutHistory() {
  const [history, setHistory] = useState<WorkoutHistoryEntry[]>([]);

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
          />
        ))}
      </div>
    </div>
  );
}

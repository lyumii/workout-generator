import { useState, useRef, useEffect } from "react";
import WorkoutCard from "./WorkoutCard";
import colors from "./colors";

export interface Exercise {
  name: string;
  sets: number;
  reps: number;
  targeted_muscles: string[];
  equipment: string;
}

export interface WorkoutHistoryEntry {
  id: number;
  prompt: string;
  timestamp: string;
  workouts: Exercise[];
}

export interface WorkoutHistoryItemProps {
  entry: WorkoutHistoryEntry;
  color?: string;
}

export default function WorkoutHistoryItem({
  entry,
  color,
}: WorkoutHistoryItemProps) {
  const [expand, setExpand] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleClickOutside = (e: MouseEvent) => {
    if (
      containerRef.current &&
      !containerRef.current.contains(e.target as Node)
    ) {
      setExpand(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div
      className="carddiv historyitemdiv"
      ref={containerRef}
      onClick={() => setExpand((prev) => !prev)}
    >
      <p
        className="title"
        style={{
          color: color,
          borderBottom: `${color} 1px solid`,
          margin: `5px`,
          fontSize: expand ? "1.2em" : "1em",
        }}
      >
        •• {entry.prompt} ••
      </p>
      {!expand && (
        <div>
          <p>
            <span className="spantitle">Targeted Muscles:</span>{" "}
            {[
              ...new Set(entry.workouts.flatMap((ex) => ex.targeted_muscles)),
            ].map((muscle, idx) => (
              <span key={idx}>| {muscle} |</span>
            ))}
          </p>
          <p>
            <span className="spantitle">Equipment used:</span>{" "}
            {[...new Set(entry.workouts.flatMap((ex) => ex.equipment))].map(
              (muscle, idx) => (
                <span key={idx}>| {muscle} |</span>
              )
            )}
          </p>
        </div>
      )}
      <div>
        {expand && (
          <div>
            {entry.workouts.map((exercise, index) => (
              <WorkoutCard
                key={index}
                name={exercise.name}
                sets={exercise.sets}
                reps={exercise.reps}
                targeted_muscles={exercise.targeted_muscles}
                equipment={exercise.equipment}
                style={{
                  borderLeft: `2px solid ${colors[index % colors.length]}`,
                  borderBottom: `2px solid ${colors[index % colors.length]}`,
                }}
                stylecolor={`${colors[index % colors.length]}`}
              />
            ))}
            <div className="buttonsdiv">
              <button
                className="buttons-categories generatedworkoutbuttons"
                style={{ backgroundColor: "#FFD166" }}
              >
                Do again
              </button>
              <button
                className="buttons-categories generatedworkoutbuttons"
                style={{ backgroundColor: "#C3E88D" }}
              >
                Edit
              </button>
              <button
                className="buttons-categories generatedworkoutbuttons"
                style={{ backgroundColor: "#4ECDC4" }}
              >
                Discard
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

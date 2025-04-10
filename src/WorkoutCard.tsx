import { useState, useEffect } from "react";
import { useEditContext } from "./EditContext";
import { useWorkoutCardContext } from "./WorkoutCardContext";

export interface WorkoutCardProps {
  id?: number;
  name: string;
  equipment?: string;
  targeted_muscles?: string[];
  sets: number;
  reps: number | string;
  className?: string;
  timestamp?: Date;
  style?: React.CSSProperties;
  stylecolor?: string;
  complete?: boolean;
  edit?: boolean;
  deleteExercise?: (id: number) => void;
}

export default function WorkoutCard(props: WorkoutCardProps) {
  const { editedExercises, setEditedExercises } = useEditContext();
  const { historyId, exerciseIndex } = useWorkoutCardContext();

  const [sets, setSets] = useState(props.sets);
  const [reps, setReps] = useState(props.reps);

  console.log(
    "WorkoutCard → historyId:",
    historyId,
    "exerciseIndex:",
    exerciseIndex
  );

  const handleChange = (field: "sets" | "reps", value: number) => {
    setEditedExercises((prev) => ({
      ...prev,
      [historyId]: {
        ...(prev[historyId] || {}),
        [exerciseIndex]: {
          ...(prev[historyId]?.[exerciseIndex] || {}),
          [field]: value,
        },
      },
    }));
  };

  useEffect(() => {
    setSets(props.sets);
    setReps(props.reps);
  }, []);

  return (
    <div className={`${props.className} editbtnsdiv`} style={props.style}>
      <div>
        <h2>
          <span style={{ color: props.stylecolor }}> • {props.name} •</span>
        </h2>
        <h3>
          <span>Equipment:</span> {props.equipment}
        </h3>
        <h3>
          <span>Targeted muscles: </span>
          {Array.isArray(props.targeted_muscles)
            ? props.targeted_muscles.join(", ")
            : props.targeted_muscles}
        </h3>
        <div className="setrepcontainer">
          <h4>
            Sets:{" "}
            {props.edit ? (
              <input
                style={{
                  backgroundColor: props.stylecolor,
                  border: "none",
                  fontWeight: "bold",
                  padding: "2px",
                  textAlign: "center",
                }}
                type="number"
                min="1"
                max="100"
                value={
                  editedExercises[historyId]?.[exerciseIndex]?.sets ??
                  props.sets
                }
                onClick={(e) => e.stopPropagation()}
                onChange={(e) => handleChange("sets", Number(e.target.value))}
              />
            ) : (
              sets
            )}
          </h4>
          <span>||</span>
          <h4>
            Reps:{" "}
            {props.edit ? (
              <input
                style={{
                  backgroundColor: props.stylecolor,
                  border: "none",
                  fontWeight: "bold",
                  padding: "2px",
                  textAlign: "center",
                }}
                type="number"
                min="1"
                max="100"
                value={
                  editedExercises[historyId]?.[exerciseIndex]?.reps ??
                  props.reps
                }
                onClick={(e) => e.stopPropagation()}
                onChange={(e) => handleChange("reps", Number(e.target.value))}
              />
            ) : (
              reps
            )}
          </h4>
        </div>
      </div>
      {props.edit && (
        <div className="buttonsdiv">
          <button
            className="buttons-categories generatedworkoutbuttons"
            style={{ backgroundColor: props.stylecolor }}
            onClick={() =>
              props.id !== undefined && props.deleteExercise?.(props.id!)
            }
          >
            Delete Exercise
          </button>
        </div>
      )}
    </div>
  );
}

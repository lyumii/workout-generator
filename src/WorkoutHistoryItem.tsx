import { useState, useRef, useEffect } from "react";
import WorkoutCard from "./WorkoutCard";
import colors from "./colors";
import { useNavigate } from "react-router-dom";
import { WorkoutCardContext } from "./WorkoutCardContext";
import { useEditContext } from "./EditContext";

export interface Exercise {
  id?: number;
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
  onDelete: () => void;
  onEdit: (id: number) => void;
  deleteBtn: (id: number, index: number) => void;
}

export default function WorkoutHistoryItem({
  entry,
  color,
  onDelete,
  onEdit,
  deleteBtn,
}: WorkoutHistoryItemProps) {
  const [expand, setExpand] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const { editedExercises, setEditedExercises } = useEditContext();
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<Exercise[]>([]);

  const containerRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  const handleClickOutside = (e: MouseEvent) => {
    if (
      containerRef.current &&
      !containerRef.current.contains(e.target as Node)
    ) {
      setExpand(false);
    }
  };
  const toggleEdit = () => {
    setIsEditing((prev) => !prev);
  };

  const handleSearch = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);

    if (value.trim() === "") {
      setSearchResults([]);
      return;
    }

    try {
      const res = await fetch(
        `http://localhost:5000/exercises/search?query=${value}`
      );
      if (!res.ok) throw new Error("Search failed :/");
      const data = await res.json();
      setSearchResults(data);
    } catch (error) {
      console.error(`Search error`, error);
      setSearchResults([]);
    }
  };

  const addExerciseFromSearch = (exercise: Exercise) => {
    setEditedExercises((prev) => {
      const current = prev[entry.id] || {};
      const nextIndex = Object.keys(current).length;

      return {
        ...prev,
        [entry.id]: {
          ...current,
          [nextIndex]: {
            sets: exercise.sets,
            reps: exercise.reps,
          },
        },
      };
    });
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
              <WorkoutCardContext.Provider
                key={index}
                value={{
                  historyId: entry.id,
                  exerciseIndex: index,
                  searchTerm,
                  setSearchTerm,
                  searchResults,
                  setSearchResults,
                  // addExerciseToWorkout,
                }}
              >
                <WorkoutCard
                  key={index}
                  name={exercise.name}
                  sets={exercise.sets}
                  reps={exercise.reps}
                  targeted_muscles={exercise.targeted_muscles}
                  equipment={exercise.equipment}
                  edit={isEditing}
                  deleteExercise={(i) => deleteBtn(entry.id, i)}
                  exerciseIndex={index}
                  style={{
                    borderLeft: `2px solid ${colors[index % colors.length]}`,
                    borderBottom: `2px solid ${colors[index % colors.length]}`,
                  }}
                  stylecolor={`${colors[index % colors.length]}`}
                />
              </WorkoutCardContext.Provider>
            ))}
            {isEditing && (
              <div className="addbox">
                <h3>Add new exercise</h3>
                <input
                  type="text"
                  value={searchTerm}
                  onChange={handleSearch}
                  onClick={(e) => e.stopPropagation()}
                />
                <ul>
                  {searchResults.map((workout) => (
                    <li key={workout.id}>
                      {workout.name}{" "}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          addExerciseFromSearch(workout);
                        }}
                      >
                        +
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <div className="buttonsdiv">
              <button
                className="buttons-categories generatedworkoutbuttons"
                style={{ backgroundColor: "#FFD166" }}
                onClick={(e) => {
                  e.preventDefault();
                  if (isEditing) {
                    e.stopPropagation();
                    console.log("ALL EDITED:", editedExercises);
                    console.log("Submitting ID:", entry.id);
                    console.log("Edited for ID:", editedExercises[entry.id]);
                    onEdit(entry.id);
                    toggleEdit();
                  } else {
                    navigate("/current", {
                      state: {
                        prompt: entry.prompt,
                        workouts: entry.workouts,
                      },
                    });
                  }
                }}
              >
                {isEditing ? "Submit Edit" : "Do Again"}
              </button>
              <button
                className="buttons-categories generatedworkoutbuttons"
                style={{ backgroundColor: "#C3E88D" }}
                onClick={(e) => {
                  e.stopPropagation();
                  toggleEdit();
                }}
              >
                {isEditing ? "Cancel Edit" : "Edit"}
              </button>
              <button
                className="buttons-categories generatedworkoutbuttons"
                style={{ backgroundColor: "#4ECDC4" }}
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete();
                }}
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

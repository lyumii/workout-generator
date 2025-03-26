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
}

export default function WorkoutHistoryItem({ entry }: WorkoutHistoryItemProps) {
  return (
    <div className="carddiv">
      <p>Prompt: {entry.prompt}</p>
      <p>
        Targeted Muscles:{" "}
        {[...new Set(entry.workouts.flatMap((ex) => ex.targeted_muscles))].map(
          (muscle, idx) => (
            <span key={idx}>| {muscle} |</span>
          )
        )}
      </p>
      <p>
        Equipment used:{" "}
        {[...new Set(entry.workouts.flatMap((ex) => ex.equipment))].map(
          (muscle, idx) => (
            <span key={idx}>| {muscle} |</span>
          )
        )}
      </p>
      {/* <div>
        {entry.workouts.map((exercise, index) => (
          <WorkoutCard
            key={index}
            name={exercise.name}
            sets={exercise.sets}
            reps={exercise.reps}
          />
        ))}
      </div> */}
    </div>
  );
}

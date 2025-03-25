import { useLocation } from "react-router-dom";
import WorkoutCard, { WorkoutCardProps } from "./WorkoutCard";

export default function GenerateWorkout() {
  const location = useLocation();
  const workouts: WorkoutCardProps[] = location.state?.workouts || [];

  return (
    <div>
      {workouts.map((workout) => (
        <WorkoutCard
          key={workout.id}
          name={workout.name}
          equipment={workout.equipment}
          targeted_muscles={workout.targeted_muscles}
          sets={workout.sets}
          reps={workout.reps}
        />
      ))}
    </div>
  );
}

export interface WorkoutCardProps {
  id?: number;
  name: string;
  equipment: string;
  targeted_muscles: string[];
  sets: number;
  reps: number | string;
}

export default function WorkoutCard(props: WorkoutCardProps) {
  return (
    <div className="carddiv">
      <h3>Exercise: {props.name}</h3>
      <p>{props.equipment}</p>
      <p>
        {Array.isArray(props.targeted_muscles)
          ? props.targeted_muscles.join(", ")
          : props.targeted_muscles}
      </p>
      <h4>Sets: {props.sets}</h4>
      <h4>Reps: {props.reps}</h4>
    </div>
  );
}

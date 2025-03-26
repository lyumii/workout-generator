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
}

export default function WorkoutCard(props: WorkoutCardProps) {
  return (
    <div className={props.className} style={props.style}>
      <h3>Exercise: {props.name}</h3>
      <p>Equipment: {props.equipment}</p>
      <p>
        Targeted muscles:
        {Array.isArray(props.targeted_muscles)
          ? props.targeted_muscles.join(", ")
          : props.targeted_muscles}
      </p>
      <div className="setrepcontainer">
        <h4>Sets: {props.sets}</h4>
        <h4>Reps: {props.reps}</h4>
      </div>
    </div>
  );
}

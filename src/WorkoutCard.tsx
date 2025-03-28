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
}

export default function WorkoutCard(props: WorkoutCardProps) {
  return (
    <div className={props.className} style={props.style}>
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
        <h4>Sets: {props.sets}</h4>
        <span>||</span>
        <h4>Reps: {props.reps}</h4>
      </div>
    </div>
  );
}

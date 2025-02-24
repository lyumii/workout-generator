interface WorkoutCardProps {
  name: string;
  sets: number;
  reps: number | string;
}

export default function WorkoutCard(props: WorkoutCardProps) {
  return (
    <div className="carddiv">
      <h3>Exercise: {props.name}</h3>
      <h4>Sets: {props.sets}</h4>
      <h4>Reps: {props.reps}</h4>
    </div>
  );
}

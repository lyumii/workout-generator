interface GenerateWorkoutProps {
  name: string;
}

const GenerateWorkout: React.FC<GenerateWorkoutProps> = (props) => {
  return <h1>Hello, {props.name}</h1>;
};

export default GenerateWorkout;

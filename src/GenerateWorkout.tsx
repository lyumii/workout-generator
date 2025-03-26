import { useLocation } from "react-router-dom";
import WorkoutCard, { WorkoutCardProps } from "./WorkoutCard";
import colors from "./colors";

export default function GenerateWorkout() {
  const location = useLocation();
  const workouts: WorkoutCardProps[] = location.state?.workouts || [];
  const prompt: string = location.state?.prompt;

  const saveWorkout = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();

    try {
      const res = await fetch("http://localhost:5000/workouthistory", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, workouts }),
      });
      if (!res.ok) {
        throw new Error(`failed to save prompt`);
      }
      console.log(`workout saved, yay`);
    } catch (error) {
      console.log(`smth went wrong`, error);
    }
  };

  return (
    <div>
      <h2 className="carddiv promptdiv">•• {prompt} ••</h2>
      <div className="exdiv">
        {workouts.map((workout: WorkoutCardProps, index) => (
          <WorkoutCard
            key={workout.id}
            name={workout.name}
            equipment={workout.equipment}
            targeted_muscles={workout.targeted_muscles}
            sets={workout.sets}
            reps={workout.reps}
            className={"generatedworkout"}
            style={{
              borderLeft: `2px solid ${colors[index % colors.length]}`,
              borderBottom: `2px solid ${colors[index % colors.length]}`,
            }}
          />
        ))}
      </div>
      <div className="buttonsdiv">
        <button
          className="buttons-categories generatedworkoutbuttons"
          style={{ backgroundColor: "#8C9EFF" }}
        >
          Let's do it!
        </button>
        <button
          className="buttons-categories generatedworkoutbuttons"
          onClick={saveWorkout}
          style={{ backgroundColor: "#67D5FF" }}
        >
          Save for later
        </button>
        <button
          className="buttons-categories generatedworkoutbuttons"
          style={{ backgroundColor: "#A29BFE" }}
        >
          Get a new one
        </button>
      </div>
    </div>
  );
}

import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState, memo } from "react";
import WorkoutCard, { WorkoutCardProps } from "./WorkoutCard";
import colors from "./colors";
import { toast } from "react-hot-toast";

function GenerateWorkout() {
  console.log("🔄 GenerateWorkout rendered");

  const location = useLocation();
  const navigate = useNavigate();

  const [workouts, setWorkouts] = useState<WorkoutCardProps[]>([]);
  const [prompt, setPrompt] = useState("");

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
      toast.success("✨ Workout added!", {
        icon: "💪",
        style: {
          background: "#333",
          color: "#fff",
          border: "1px solid #F5A623",
        },
      });
      console.log(`workout saved, yay`);
    } catch (error) {
      console.log(`smth went wrong`, error);
    }
  };

  const cardStyles = workouts.map((_, index) => ({
    borderLeft: `2px solid ${colors[index % colors.length]}`,
    borderBottom: `2px solid ${colors[index % colors.length]}`,
  }));

  const styleColors = workouts.map((_, index) => colors[index % colors.length]);

  useEffect(() => {
    if (location.state) {
      setWorkouts(location.state.workouts || []);
      setPrompt(location.state.prompt || "");
    }
  }, []);

  return (
    <div className="generatedworkoutswidth">
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
            style={cardStyles[index]}
            stylecolor={styleColors[index]}
          />
        ))}
      </div>
      <div className="buttonsdiv">
        <button
          className="buttons-categories generatedworkoutbuttons"
          style={{ backgroundColor: "#8C9EFF" }}
          onClick={(e) => {
            e.preventDefault();
            navigate("/current", {
              state: {
                prompt,
                workouts,
              },
            });
          }}
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

export default memo(GenerateWorkout);

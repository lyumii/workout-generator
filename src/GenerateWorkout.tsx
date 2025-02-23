import WorkoutLibrary from "./WorkoutLibrary";
import React from "react";
import WorkoutCard from "./WorkoutCard";

interface GenerateWorkoutProps {
  name: string;
}

export default function GenerateWorkout(props: GenerateWorkoutProps) {
  // const [upperBodyFilter, setUpperBodyFilter] = React.useState(false);
  // const [lowerBodyFilter, setLowerBodyFilter] = React.useState(false);
  // const [fullBodyFilter, setFullBodyFilter] = React.useState(false);
  // const [coreFilter, setCoreFilter] = React.useState(false);
  // const [mobilityFilter, setMobilityFilter] = React.useState(false);
  // const [beginnerFilter, setBeginnerFilter] = React.useState(true);
  // const [intermediateFilter, setIntermediateFilter] = React.useState(false);
  // const [advancedFilter, setAdvancedFilter] = React.useState(false);
  const [filters, setFilters] = React.useState({
    upperBody: false,
    lowerBody: false,
    fullBody: false,
    core: false,
    mobility: false,
    beginner: true,
    intermediate: false,
    advanced: false,
  });

  const activeFilters = {
    "Upper Body": filters.upperBody,
    Legs: filters.lowerBody,
    "Full Body": filters.fullBody,
    Core: filters.core,
    Mobility: filters.mobility,
    Beginner: filters.beginner,
    Intermediate: filters.intermediate,
    Advanced: filters.advanced,
  };

  const filteredWorkout = () => {
    const categoriedWorkout = WorkoutLibrary.filter((item) => {
      return Object.entries(activeFilters).some(
        ([key, value]) => value && item.category === key
      );
    });

    const difficultyFiltered = categoriedWorkout.filter((item) => {
      return Object.entries(activeFilters).some(
        ([key, value]) => value && item.difficulty === key
      );
    });
    return categoriedWorkout && difficultyFiltered;
  };

  const handleCategoryClick = (category: keyof typeof filters) => {
    setFilters((prev) => ({
      ...prev,
      upperBody: false,
      lowerBody: false,
      fullBody: false,
      core: false,
      mobility: false,
      [category]: true,
    }));
  };

  const handleDifficultyClick = (difficulty: keyof typeof filters) => {
    setFilters((prev) => ({
      ...prev,
      beginner: false,
      intermediate: false,
      advanced: false,
      [difficulty]: true,
    }));
  };

  return (
    <>
      <h1>Hello, {props.name}</h1>
      <h2>What would you like to do today?</h2>
      <div>
        <button onClick={() => handleCategoryClick("upperBody")}>
          Upper Body
        </button>
        <button onClick={() => handleCategoryClick("lowerBody")}>
          Lower Body
        </button>
        <button onClick={() => handleCategoryClick("fullBody")}>
          Full Body
        </button>
        <button onClick={() => handleCategoryClick("core")}>Core</button>
        <button onClick={() => handleCategoryClick("mobility")}>
          Mobility
        </button>
      </div>
      <div>
        <button onClick={() => handleDifficultyClick("beginner")}>
          Beginner
        </button>
        <button onClick={() => handleDifficultyClick("intermediate")}>
          Intermediate
        </button>
        <button onClick={() => handleDifficultyClick("advanced")}>
          Advanced
        </button>
      </div>
      <div>
        {filteredWorkout().map((item) =>
          item.workouts.map((workout, workoutIndex) => (
            <WorkoutCard
              key={`${workout.name}-${workoutIndex}`}
              name={workout.name}
              sets={workout.sets}
              reps={workout.sets}
            />
          ))
        )}
      </div>
    </>
  );
}

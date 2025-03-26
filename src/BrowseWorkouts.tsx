import WorkoutLibrary from "./WorkoutLibrary";
import React from "react";
import WorkoutCard from "./WorkoutCard";

export default function BrowseWorkouts() {
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
      <div className="buttons-categories">
        <button
          onClick={() => handleCategoryClick("upperBody")}
          className={filters.upperBody ? "selected" : ""}
          style={{ backgroundColor: "#F5A623" }}
        >
          Upper Body
        </button>
        <button
          onClick={() => handleCategoryClick("lowerBody")}
          className={filters.lowerBody ? "selected" : ""}
          style={{ backgroundColor: "#FFD166" }}
        >
          Lower Body
        </button>
        <button
          onClick={() => handleCategoryClick("fullBody")}
          className={filters.fullBody ? "selected" : ""}
          style={{ backgroundColor: "#06D6A0" }}
        >
          Full Body
        </button>
        <button
          onClick={() => handleCategoryClick("core")}
          className={filters.core ? "selected" : ""}
          style={{ backgroundColor: "#4ECDC4" }}
        >
          Core
        </button>
        <button
          onClick={() => handleCategoryClick("mobility")}
          className={filters.mobility ? "selected" : ""}
          style={{ backgroundColor: "#C3E88D" }}
        >
          Mobility
        </button>
      </div>
      <div className="buttons-difficulty">
        <button
          onClick={() => handleDifficultyClick("beginner")}
          className={filters.beginner ? "selected" : ""}
          style={{ backgroundColor: "#A29BFE" }}
        >
          Beginner
        </button>
        <button
          onClick={() => handleDifficultyClick("intermediate")}
          className={filters.intermediate ? "selected" : ""}
          style={{ backgroundColor: "#8C9EFF" }}
        >
          Intermediate
        </button>
        <button
          onClick={() => handleDifficultyClick("advanced")}
          className={filters.advanced ? "selected" : ""}
          style={{ backgroundColor: "#67D5FF" }}
        >
          Advanced
        </button>
      </div>
      <div>
        {(() => {
          const filteredWorkouts = filteredWorkout();

          if (!filteredWorkouts.length) {
            return (
              <p className="notavailablep">
                No workout available with those filters
              </p>
            );
          }

          return filteredWorkouts.map((item) =>
            item.workouts.map((workout, workoutIndex) => (
              <WorkoutCard
                key={`${workout.name}-${workoutIndex}`}
                name={workout.name}
                sets={workout.sets}
                reps={workout.reps ?? "N/A"}
                className={"carddiv"}
              />
            ))
          );
        })()}
      </div>
    </>
  );
}

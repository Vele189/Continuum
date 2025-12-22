

@router.patch("/{task_id}/milestone", response_model=Task)
def link_milestone(
    task_id: int,
    link_request: MilestoneLinkRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Link or unlink a task from a milestone.
    """
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify project membership (admins bypass)
    if not is_admin_user(current_user):
        if not task_service.validate_project_membership(db, task.project_id, current_user.id):
            raise HTTPException(status_code=403, detail="Not a member of this project")

    if link_request.milestone_id is not None:
        milestone = MilestoneService.get(db, link_request.milestone_id)
        if not milestone:
            raise HTTPException(status_code=404, detail="Milestone not found")
        
        # Cross-project validation
        if milestone.project_id != task.project_id:
            raise HTTPException(status_code=400, detail="Cannot link task to milestone in different project")

    update_data = TaskUpdate(milestone_id=link_request.milestone_id)
    updated_task = task_service.update(db, db_obj=task, obj_in=update_data)
    
    if updated_task.milestone_id:
         ms = MilestoneService.get(db, updated_task.milestone_id)
         if ms:
             MilestoneService.update_status(db, ms)
    
    return updated_task

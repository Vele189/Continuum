
@router.get("/{project_id}/milestones", response_model=List[Milestone])
def list_project_milestones(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List milestones for a project.

    - Admins can view milestones of any project
    - Members can view milestones of projects they belong to
    """
    is_admin = is_admin_user(current_user)
    # Verify access to project first
    ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)
    
    milestones = MilestoneService.get_by_project(db, project_id)
    
    # Enrichment with progress
    results = []
    for m in milestones:
        MilestoneService.update_status(db, m)
        progress = MilestoneService.calculate_progress(db, m.id)
        
        # Pydantic model conversion
        # We need to construct the response manually to inject progress, or rely on pydantic validtion if property set
        # Since 'm' is SQLAlchemy model, we can attach the dict but pydantic v2 is stricter.
        # But 'Milestone' schema has 'progress' field.
        
        res = Milestone.model_validate(m)
        res.progress = progress
        results.append(res)
        
    return results

<template>
    <div class="modal fade" id="rename" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 id="rename-title">重命名</h5>
                </div>
                <div class="modal-body">
                    <form class="input-group">
                        <div class="input-group-append">
                            <span class="input-group-text">新名称：</span>
                        </div>
                        <input type="text" id="rename-input" class="form-control" name="newname">
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" id="rename-button">确定</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                </div>
            </div>
        </div>
    </div>
</template>

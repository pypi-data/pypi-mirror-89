"""Test basic CLI commands that create Honeybee Models."""
import sys
import json
from click.testing import CliRunner

from honeybee.model import Model
from honeybee.boundarycondition import Outdoors, Ground
from honeybee.cli.create import shoe_box, rectangle_plan


def test_shoe_box_simple():
    runner = CliRunner()
    result = runner.invoke(shoe_box, ['5', '10', '3.5'])
    assert result.exit_code == 0

    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert len(new_model.rooms) == 1
    assert len(new_model.apertures) == 0


def test_shoe_box_detailed():
    runner = CliRunner()
    in_arg = ['15', '30', '9', '-a', '180', '-wr', '0.6', '-o', '-u', 'Feet']
    result = runner.invoke(shoe_box, in_arg)
    assert result.exit_code == 0

    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert new_model.units == 'Feet'
    assert len(new_model.rooms) == 1
    assert all(isinstance(face.boundary_condition, (Outdoors, Ground))
               for face in new_model.faces)
    assert len(new_model.apertures) == 1
    assert new_model.apertures[0].cardinal_direction() == 'South'


def test_rectangle_plan_simple():
    runner = CliRunner()
    result = runner.invoke(rectangle_plan, ['30', '20', '3.5'])
    assert result.exit_code == 0
    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert len(new_model.rooms) == 1
    assert len(new_model.apertures) == 0

    result = runner.invoke(rectangle_plan, ['30', '20', '3.5', '-p', '5'])
    assert result.exit_code == 0
    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert len(new_model.rooms) == 5

    result = runner.invoke(rectangle_plan, ['30', '20', '3.5', '-p', '10'])
    assert result.exit_code == 0
    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert len(new_model.rooms) == 4


def test_rectangle_plan_detailed():
    runner = CliRunner()
    in_arg = ['100', '50', '10', '-p', '15', '-s', '3', '-a', '45', '-u', 'Feet']
    result = runner.invoke(rectangle_plan, in_arg)
    assert result.exit_code == 0
    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert new_model.units == 'Feet'
    assert len(new_model.rooms) == 15
    assert len(new_model.apertures) == 0
    assert all(isinstance(face.boundary_condition, (Outdoors, Ground))
               for face in new_model.faces)


def test_rectangle_plan_detailed():
    runner = CliRunner()
    in_arg = ['30', '20', '3.5', '-p', '5', '-a', '135', '-ar', '-af']
    result = runner.invoke(rectangle_plan, in_arg)
    assert result.exit_code == 0
    model_dict = json.loads(result.output)
    new_model = Model.from_dict(model_dict)
    assert new_model.units == 'Meters'
    assert len(new_model.rooms) == 5
    assert len(new_model.apertures) == 0
